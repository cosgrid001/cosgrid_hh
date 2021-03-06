# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
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


from django.template.defaultfilters import capfirst
from django.template.defaultfilters import floatformat
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from hpcloud import usage
from hpcloud.usage import base
from horizon import forms
from hpcloud.overview import forms as project_forms
from django.core.urlresolvers import reverse_lazy
from hpcloud.api.base import get_accounts


class ProjectUsageCsvRenderer(base.BaseCsvResponse):

    columns = [_("Instance Name"), _("VCPUs"), _("Ram (MB)"),
               _("Disk (GB)"), _("Usage (Hours)"),
               _("Uptime(Seconds)"), _("State")]

    def get_row_data(self):

        for inst in self.context['usage'].get_instances():
            yield (inst['name'],
                   inst['vcpus'],
                   inst['memory_mb'],
                   inst['local_gb'],
                   floatformat(inst['hours'], 2),
                   inst['uptime'],
                   capfirst(inst['state']))


class ProjectOverview(usage.UsageView):
    table_class = usage.ProjectUsageTable
    usage_class = usage.ProjectUsage
    template_name = 'hpcloud/overview/usage.html'
    csv_response_class = ProjectUsageCsvRenderer

    def get_data(self):
        super(ProjectOverview, self).get_data()
        return self.usage.get_instances()


class WarningView(TemplateView):
    template_name = "hpcloud/_warning.html"

class AccountChange(forms.ModalFormView):
    form_class = project_forms.AccountChangeForm
    template_name = 'hpcloud/account.html'
    success_url = reverse_lazy('horizon:hpcloud:overview:index')
     
    def get_initial(self):
        hp_accounts = get_accounts(self.request)
        return { 'account_choices':hp_accounts }
