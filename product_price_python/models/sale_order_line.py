# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line',

    @api.depends('price_unit')
    def get_product_unit_python_price(self):
        for record in self:
            if (record.product_id.tipo_calculo == 'personal'):

                # Inicialización:
                inicio_extra = record.incio_extra
                inicio_ordinario = record.inicio_ordinario
                final_ordinario = record.final_ordinario
                final_extra = record.final_hextra
                hextra_factor = record.hextra_factor
                hfestivo_factor = record.hfestivo_factor
                horas_minimo = record.horas_minimo
                hextras, hlaborales, festivos, laborables = 0, 0, 0, 0

                fecha = datetime.datetime(year=record.start_date.year, month=record.start_date.month,
                                          day=record.start_date.day,
                                          hour=record.start_date.hour, minute=record.start_date.minute)
                empieza_jornada = datetime.datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=incio_extra,
                                                    minute=0)
                termina_jornada = datetime.datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=final_extra,
                                                    minute=0)

                # Calculate local time diference with UTC:
                date = datetime.datetime.today()
                date_today = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=12, minute=0)
                date_utc = date_today.astimezone(timezone(user.tz))
                inc = date_utc.hour - date_today.hour

                # Número de días contratados:
                ndias = (record.return_date - record.start_date).days + 1

                # Fijar franja horaria cada media hora y como máximo empezamos en hmincontratable:
                empieza = fecha + datetime.timedelta(hours=inc)
                empieza_minimo = datetime.datetime(year=fecha.year, month=fecha.month, day=fecha.day,
                                                   hour=hmincontratable,
                                                   minute=0)

                if empieza.hour < empieza_minimo.hour:
                    empieza = empieza_minimo

                if (empieza.minute < 30):
                    empieza += datetime.timedelta(minutes=-empieza.minute)
                if (empieza.minute > 30):
                    empieza = datetime.datetime(year=empieza.year, month=empieza.month, day=empieza.day,
                                                hour=empieza.hour,
                                                minute=30)

                # Cantidad de horas extras por la mañana:
                iniciojornada = datetime.datetime(year=empieza.year, month=empieza.month, day=empieza.day,
                                                  hour=inicio_ordinario,
                                                  minute=0)
                dif = (iniciojornada - empieza).total_seconds() / 3600.0
                if (dif > 0) and (dif > inicio_ordinario - hmincontratable):  hextras += (
                            inicio_ordinario - hmincontratable)
                if (dif > 0) and (dif <= inicio_ordinario - hmincontratable):
                    hextras += dif
                else:
                    hextras += 0

                # Horas extras por la noche, teniendo en cuenta el horario de cierre:
                termina = record.return_date + datetime.timedelta(hours=inc)
                termina = datetime.datetime(year=empieza.year, month=empieza.month, day=empieza.day,
                                            hour=termina.hour, minute=termina.minute)
                termina_maximo = datetime.datetime(year=termina.year, month=termina.month, day=termina.day,
                                                   hour=final_extra, minute=0)
                if termina.hour > termina_maximo.hour:
                    termina = termina_maximo

                if (termina.minute > 30):
                    termina += datetime.timedelta(minutes=60 - termina.minute)
                if (termina.minute < 30) and (termina.minute != 0):
                    termina = datetime.datetime(year=termina.year, month=termina.month, day=termina.day,
                                                hour=termina.hour,
                                                minute=30)

                finjornada = datetime.datetime(year=termina.year, month=termina.month, day=termina.day,
                                               hour=final_ordinario, minute=0)
                dif = (termina - finjornada).total_seconds() / 3600.0

                if (dif > 0) and (dif > final_extra - final_ordinario):  hextras += (final_extra - final_ordinario)
                if (dif > 0) and (dif <= final_extra - final_ordinario):
                    hextras += dif
                else:
                    hextras += 0

                # En horario laboral:
                hlaborales = (termina - empieza).total_seconds() / 3600.0 - hextras

                if (hlaborales + hextras) < horas_minimo:
                    hlaborales = horas_minimo - hextras

                # Festivos/laborables (pendiente):
                date_list = [record.return_date.date() - datetime.timedelta(days=x) for x in range(ndias)]
                for date in date_list:
                    if (user.company_id.festivos) and (str(date) in user.company_id.festivos) or (date.weekday() == 6):
                        festivos += 1
                laborables = ndias - festivos

                # Cálculo coste total por día (laborable + festivos):
                precio = record.product_id.list_price
                subtotal_dia = precio * (hlaborales + hextras * record.product_id.hextra_factor)
                total = subtotal_dia * (laborables + festivos * record.product_id.hfestivo_factor)

                # Escritura del total, si procede:
                if (record.price_unit != total):
                    record['price_unit'] = total

