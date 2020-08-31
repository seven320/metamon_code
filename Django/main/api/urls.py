from rest_framework import routers
from .views import UserViewSet, TaskViewSet, Task_historyViewSet
from .views import SearchUserViewSet, SearchTaskViewSet, SearchTask_historyViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('tasks', TaskViewSet)
router.register('task_historys', Task_historyViewSet)

# 検索
router.register('search/users', SearchUserViewSet)
router.register('search/tasks', SearchTaskViewSet)
router.register('search/task_historys', SearchTask_historyViewSet)

urlpatterns = router.urls