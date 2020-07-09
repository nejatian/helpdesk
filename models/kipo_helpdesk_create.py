# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class KipoHelpdeskTags(models.Model):
    _name = 'kipo.helpdesk.create.tags'
    name = fields.Char()


class KipoHelpdeskDevices(models.Model):
    _name = 'kipo.helpdesk.create.devices'
    name = fields.Char()


class KipoHelpdeskVersions(models.Model):
    _name = 'kipo.helpdesk.create.versions'
    name = fields.Char()


class KipoHelpdeskCreate(models.Model):
    _name = 'kipo.helpdesk.create'

    customer_name = fields.Char(string='Customer Name')
    kipo_num = fields.Char(string='Kipo Number', required=True)
    tel_number = fields.Char(string='Tel', required=True)
    email = fields.Char(string='Email')
    device_id = fields.Many2one('kipo.helpdesk.create.devices', string='Device')
    version_id = fields.Many2one('kipo.helpdesk.create.versions', string='Version')
    problem_des = fields.Text(string='Problem Description', required=True)
    tag_id = fields.Many2one('kipo.helpdesk.create.tags', string='Tag')
    assignedto_id = fields.Many2one('res.users', string='Assigned to', required=True)

    @api.multi
    def create_helpdesk_card(self):
        condition = [('name', '=', 'Helpdesk')]
        res = self.env['project.project'].search(condition)
        if len(res) != 0:
            projectId = res[0]['id']

            if self.customer_name == False:
                customerName = ''
            else:
                customerName = str(self.customer_name)

            if self.kipo_num == False:
                kipoNum = ''
            else:
                kipoNum = str(self.kipo_num)

            if self.tel_number == False:
                telNumber = ''
            else:
                telNumber = str(self.tel_number)

            if self.email == False:
                customerEmail = ''
            else:
                customerEmail = str(self.email)

            version = ''
            condition = [('id', '=', int(self.version_id))]
            res = self.env['kipo.helpdesk.create.versions'].search(condition)
            if len(res) != 0:
                version = res[0]['name']

            device = ''
            condition = [('id', '=', int(self.device_id))]
            res = self.env['kipo.helpdesk.create.devices'].search(condition)
            if len(res) != 0:
                device = res[0]['name']

            tag = ''
            condition = [('id', '=', int(self.tag_id))]
            res = self.env['kipo.helpdesk.create.tags'].search(condition)
            if len(res) != 0:
                tag = res[0]['name']

            if self.problem_des == False:
                problemDes = ''
            else:
                problemDes = str(self.problem_des)

            correctDes = '<p>'
            for i in range(len(problemDes)):
                tempChar = problemDes[i]

                newLineFound = False
                if ord(tempChar) == 10:
                    newLineFound = True

                if newLineFound:
                    correctDes = correctDes + '</p><p>'
                else:
                    correctDes = correctDes + tempChar
            correctDes = correctDes + '</p>'

            fullDescription = "<p>" + "Customer Name:" + customerName + "</p>"
            fullDescription = fullDescription + "<p>" + "Kipo Num:" + kipoNum + "</p>"
            fullDescription = fullDescription + "<p>" + "Tel:" + telNumber + "</p>"
            fullDescription = fullDescription + "<p>" + "Email:" + customerEmail + "</p>"
            fullDescription = fullDescription + "<p>" + "Version:" + version + "</p>"
            fullDescription = fullDescription + "<p>" + "Device:" + device + "</p>"
            fullDescription = fullDescription + "<p>" + "Tag:" + tag + "</p>"
            fullDescription = fullDescription + "<p>" + "Description:" + "</p>"
            fullDescription = fullDescription + correctDes

            newProjectTask = {}
            newProjectTask['project_id'] = projectId
            newProjectTask['name'] = kipoNum
            newProjectTask['description'] = fullDescription
            newProjectTask['user_id'] = int(self.assignedto_id)

            record = self.env['project.task'].create(newProjectTask)

        return {
            'view_type': 'form',
            'view_id': self.env.ref('kipo_helpdesk_create.action_kipo_helpdesk_create_view_form').id,
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'kipo.helpdesk.create',
            'type': 'ir.actions.act_window',
            'target': 'new'}
