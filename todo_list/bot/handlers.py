from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tasks.models import Task, Profile


@csrf_exempt
def link_account(request):
    if request.method == 'POST':
        tg_username = request.POST['tg_username']
        code = request.POST['code']
        try:
            profile = Profile.objects.get(code=code)
            profile.tg_username = tg_username
            profile.save()
            return JsonResponse({"message": "Account linked successfully"}, status=200)
        except Profile.DoesNotExist:
            return JsonResponse({"error": "Unique code does not exist"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        tg_username = request.POST.get('tg_username')
        title = request.POST.get('title')
        description = request.POST.get('description')
        try:
            profile = Profile.objects.get(tg_username=tg_username)
            task = Task.objects.create(user=profile.user, title=title, description=description)
            return JsonResponse({"status": "success", "task_id": task.id}, status=201)
        except Profile.DoesNotExist:
            return JsonResponse({"error": "Telegram ID does not exist"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def get_tasks(request):
    if request.method == 'GET':
        tg_username = request.GET.get('tg_username')
        try:
            profile = Profile.objects.get(tg_username=tg_username)
            tasks = Task.objects.filter(user=profile.user)
            tasks_list = [
                {"id": task.id, "title": task.title, "description": task.description, "completed": task.completed} for
                task in tasks]
            return JsonResponse(tasks_list, safe=False)
        except Profile.DoesNotExist:
            return JsonResponse({"error": "Telegram ID does not exist"}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)