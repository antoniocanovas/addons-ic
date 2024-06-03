/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import { registry } from "@web/core/registry";
import { CopyClipboardCharField } from "@web/views/fields/copy_clipboard/copy_clipboard_field"
import { archParseBoolean } from "@web/views/utils";


CopyClipboardCharField.props = {
    ...CopyClipboardCharField.props,
    isPassword: { type: Boolean, optional: true },
};

CopyClipboardCharField.extractProps = ({ attrs, field }) => {
    return {
        isPassword: archParseBoolean(attrs.password),
    };
};

patch(CopyClipboardCharField.prototype, "CopyClipboardCharField.password", {
    get isPassword() {
        return this.props.isPassword;
    }
});