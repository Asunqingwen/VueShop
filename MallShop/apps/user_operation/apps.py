from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = '操作管理'

    def ready(self):
        """
        信号设置
        :return:
        """
        import user_operation.signals
