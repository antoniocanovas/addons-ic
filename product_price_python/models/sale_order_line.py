# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line',

    @api.depends('price_unit')
    def get_product_unit_python_price(self):
        for record in self:
            raise UserError('funciona')
            # Inicialización:
            hmincontratable, hinicio, hfin, hmaxcontratable, hextras, hlaborales, hmincontrato, festivos, laborables = 7, 8, 20, 22, 0, 0, 4, 0, 0
            fecha = datetime.datetime(year=record.start_date.year, month=record.start_date.month, day=record.start_date.day,
                                      hour=record.start_date.hour, minute=record.start_date.minute)
            empieza_jornada = datetime.datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hmincontratable,
                                                minute=0)
            termina_jornada = datetime.datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hmaxcontratable,
                                                minute=0)

            # Calculate local time diference with UTC:
            date = datetime.datetime.today()
            date_today = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=12, minute=0)
            date_utc = date_today.astimezone(timezone(user.tz))
            inc = date_utc.hour - date_today.hour

            # Número de días contratados:
            ndias = (record.return_date - record.start_date).days + 1

            # Fijar franja horaria cada media hora y como máximo empezamos en hmincontratable:
            empieza = datetime.datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=(fecha.hour + inc),
                                        minute=fecha.minute)
            empieza_minimo = datetime.datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hmincontratable,
                                               minute=0)
            if empieza.hour < empieza_minimo.hour:
                empieza = empieza_minimo

            if (empieza.minute < 30):
                empieza += datetime.timedelta(minutes=-empieza.minute)
            if (empieza.minute > 30):
                empieza = datetime.datetime(year=empieza.year, month=empieza.month, day=empieza.day, hour=empieza.hour,
                                            minute=30)

            # Cantidad de horas extras por la mañana:
            iniciojornada = datetime.datetime(year=empieza.year, month=empieza.month, day=empieza.day, hour=hinicio,
                                              minute=0)
            dif = (iniciojornada - empieza).total_seconds() / 3600.0
            if (dif > 0) and (dif > hinicio - hmincontratable):  hextras += (hinicio - hmincontratable)
            if (dif > 0) and (dif <= hinicio - hmincontratable):
                hextras += dif
            else:
                hextras += 0

            # Horas extras por la noche, teniendo en cuenta el horario de cierre:
            termina = datetime.datetime(year=empieza.year, month=empieza.month, day=empieza.day,
                                        hour=(record.return_date.hour + inc), minute=record.return_date.minute)
            termina_maximo = datetime.datetime(year=termina.year, month=termina.month, day=termina.day,
                                               hour=hmaxcontratable, minute=0)
            if termina.hour > termina_maximo.hour:
                termina = termina_maximo

            if (termina.minute > 30):
                termina += datetime.timedelta(minutes=60 - termina.minute)
            if (termina.minute < 30) and (termina.minute != 0):
                termina = datetime.datetime(year=termina.year, month=termina.month, day=termina.day, hour=termina.hour,
                                            minute=30)

            finjornada = datetime.datetime(year=termina.year, month=termina.month, day=termina.day, hour=hfin, minute=0)
            dif = (termina - finjornada).total_seconds() / 3600.0

            if (dif > 0) and (dif > hmaxcontratable - hfin):  hextras += (hmaxcontratable - hfin)
            if (dif > 0) and (dif <= hmaxcontratable - hfin):
                hextras += dif
            else:
                hextras += 0

            # En horario laboral:
            hlaborales = (termina - empieza).total_seconds() / 3600.0 - hextras

            if (hlaborales + hextras) < hmincontrato:
                hlaborales = hmincontrato - hextras

            # Festivos/laborables (pendiente):
            date_list = [record.return_date.date() - datetime.timedelta(days=x) for x in range(ndias)]
            for date in date_list:
                if (str(date) in user.company_id.x_studio_festivos) or (date.weekday() == 6):
                    festivos += 1
            laborables = ndias - festivos

            # Cálculo coste total por día (laborable + festivos):
            precio = record.product_id.list_price
            subtotal_dia = precio * (hlaborales + hextras * record.product_id.x_studio_extra)
            total = subtotal_dia * (laborables + festivos * record.product_id.x_studio_festivo)

            # Escritura del total, si procede:
            if (record.price_unit != total):
                record['price_unit'] = total
            else: return True
            # self.price_unit = 888

