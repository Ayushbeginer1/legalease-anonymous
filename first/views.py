from .models import AnonymousTip
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, HttpResponseForbidden
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AnonymousTipSerializer
import json
from django.shortcuts import render, get_object_or_404
import os

@csrf_exempt
def submit_anonymous_tip(request):
    if request.method == "POST":
        try:
            category = request.POST.get("category")
            urgency = request.POST.get("urgency")
            location = request.POST.get("location")
            description = request.POST.get("description")
            evidence = request.FILES.get("evidence")

            # --- Limit and check file upload ---
            MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
            ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf']

            if evidence:
                ext = os.path.splitext(evidence.name)[1].lower()
                if ext not in ALLOWED_EXTENSIONS:
                    return JsonResponse({"error": "❌ File type not allowed."}, status=400)

                if evidence.size > MAX_UPLOAD_SIZE:
                    return JsonResponse({"error": "❌ File too large. Max 5MB allowed."}, status=400)

            # --- Limit to 500 tips in DB ---
            MAX_TIPS = 500
            if AnonymousTip.objects.count() >= MAX_TIPS:
                oldest = AnonymousTip.objects.earliest('submitted_at')
                oldest.delete()


            tip = AnonymousTip.objects.create(
                category=category,
                urgency=urgency,
                location=location,
                description=description,
                evidence=evidence if evidence else None
            )
            print("✅ Tip saved:", tip)
            return JsonResponse({"message": "Tip submitted successfully!",
            "access_key": str(tip.access_key)}, status=201)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"error": f"Invalid data: {str(e)}"}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)

def list_public_tips(request):
    if request.method == "GET":
        tips = AnonymousTip.objects.all().values()
        return JsonResponse(list(tips), safe=False)
    return JsonResponse({'error': 'Only GET allowed'}, status=405)

def show_all_tips(request):
    tips = AnonymousTip.objects.all().order_by('-submitted_at')
    return render(request, 'C:/Users/Ayush/backend/anonymous/first/templates/public.html', {'tips': tips})

def download_evidence(request, access_key):
    try:
        tip = AnonymousTip.objects.get(access_key=access_key)

        if not tip.evidence:
            raise Http404("No evidence file found.")

        file_path = tip.evidence.path

        if not os.path.exists(file_path):
            raise Http404("File does not exist.")

        return FileResponse(open(file_path, 'rb'), as_attachment=True)

    except AnonymousTip.DoesNotExist:
        raise Http404("Tip not found.")
    except Exception as e:
        from django.http import JsonResponse
        return JsonResponse({'error': str(e)}, status=403)