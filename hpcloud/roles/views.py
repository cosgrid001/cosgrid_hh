# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import exceptions,forms,tables
from openstack_dashboard import api
from hpcloud.roles \
    import forms as project_forms
from hpcloud.roles \
    import tables as project_tables


class IndexView(tables.DataTableView):
    table_class = project_tables.RolesTable
    template_name = 'hpcloud/roles/index.html'

    def get_data(self):
        roles = []
        try:
            roles = api.keystone.role_list(self.request)
        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve roles list.'))
        return roles


class UpdateView(forms.ModalFormView):
    form_class = project_forms.UpdateRoleForm
    template_name = 'hpcloud/roles/update.html'
    success_url = reverse_lazy('horizon:hpcloud:roles:index')

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object = api.keystone.role_get(self.request,
                                                     self.kwargs['role_id'])
            except Exception:
                redirect = reverse("horizon:hpcloud:roles:index")
                exceptions.handle(self.request,
                                  _('Unable to update role.'),
                                  redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['role'] = self.get_object()
        return context

    def get_initial(self):
        role = self.get_object()
        return {'id': role.id,
                'name': role.name}


class CreateView(forms.ModalFormView):
    form_class = project_forms.CreateRoleForm
    template_name = 'hpcloud/roles/create.html'
    success_url = reverse_lazy('horizon:hpcloud:roles:index')
