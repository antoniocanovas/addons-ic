odoo.define('pos_table_state.TableInfoPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class TableInfoPopup extends AbstractAwaitablePopup {
    }
    TableInfoPopup.template = 'TableInfoPopup';
    TableInfoPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: 'Table Information',
        body: '',
    };
    Registries.Component.add(TableInfoPopup);
    return TableInfoPopup;
});
