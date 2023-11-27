from templated_mail.mail import BaseEmailMessage


class IncomesApproveEmail(BaseEmailMessage):
    template_name = 'email/incomes_approve.html'

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get('user')
        project = context.get('project')
        date_time = context.get('date_time')
        context.update({
            'user': user,
            'project': project,
            'date_time': date_time,
        })
        return context
