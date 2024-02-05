URLS = {
    'auth': {
        'login': '/auth/login',
        'info': '/auth/info',
    },
    'user': {
        'create_user': '/users/signup',
        'get_put_del_user_by_id': '/users/{user_id}',
        'get_me': '/users/me',
        'get_my_subscriptions': '/users/me/subscriptions',
        'get_user_subscriptions_by_id': '/users/{user_id}/subscriptions',
    },
    'course': {
        'get_post_courses': '/courses',
        'get_put_del_course_by_id': '/courses/{course_id}',
        'get_subscribers': '/courses/{course_id}/subscribers',
        'subscribe_to_course': '/courses/{course_id}/subscribe',
    },
    'lesson': {
        'get_post_lessons': '/courses/{course_id}/lessons',
        'get_put_del_lesson_by_id': '/courses/{course_id}/lessons/{lesson_id}',
    },
}
