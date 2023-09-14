from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect(reverse_lazy('news'))


class BaseUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'edit.html'
    success_url = reverse_lazy('news')

    def get_object(self, queryset=None):
        return self.request.user
