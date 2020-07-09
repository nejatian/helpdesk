import werkzeug

from odoo import http, models

from odoo.http import request


class HelpDesk(http.Controller):
    @http.route('/helpdesk', website=True, auth='public')
    def helpdesk(self, **kw):
        return http.request.render('kipo_helpdesk_create.helpdesk_page', {})

    @http.route('/ticketprocess', type="http", auth="public", website=True)
    def support_process_ticket(self, **kwargs):
        values = {}
        for field_name, field_value in kwargs.items():
            values[field_name] = field_value

        if values['my_gold'] != "256":
            return "Bot Detected"

        condition = [('name', '=', 'HelpDesk')]
        res = request.env['project.project'].search(condition)
        if len(res) != 0:
            projectId = res[0]['id']
        userCondition =[('name', '=', 'Administrator')]
        userID=request.env['res.users'].search(userCondition)

        if values['customer_name'] == False:
            customerName = ''
        else:
            customerName = str(values['customer_name'])

        if values['tel_number'] == False:
            telNumber = ''
        else:
            telNumber = str(values['tel_number'])

        if values['email'] == False:
            customerEmail = ''
        else:
            customerEmail = str(values['email'])

        if values['problemDes'] == False:
            problemDes = ''
        else:
            problemDes = str(values['problemDes'])

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
        fullDescription = fullDescription + "<p>" + "Tel:" + telNumber + "</p>"
        fullDescription = fullDescription + "<p>" + "Email:" + customerEmail + "</p>"
        fullDescription = fullDescription + "<p>" + "Description:" + "</p>"
        fullDescription = fullDescription + correctDes

        newProjectTask = {}
        newProjectTask['project_id'] = projectId
        newProjectTask['name'] = telNumber
        newProjectTask['description'] = fullDescription
        newProjectTask['user_id'] = int(userID)

        record = request.env['project.task'].create(newProjectTask)
        return werkzeug.utils.redirect("/helpdesk")
