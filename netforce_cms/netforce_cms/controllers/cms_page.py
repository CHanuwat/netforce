# Copyright (c) 2012-2015 Netforce Co. Ltd.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

from netforce.controller import Controller
from netforce.template import render
from netforce.model import get_model
from netforce.database import get_connection,get_active_db # XXX: move this
from netforce.locale import set_active_locale,get_active_locale
from .cms_base import BaseController

class Page(BaseController):
    _path="/cms_page"

    def get(self):
        db=get_connection()
        try:
            ctx=self.context
            page_code=self.get_argument("page")
            res=get_model("cms.page").search([["code","=",page_code]])
            if not res:
                self.redirect("/cms_page_not_found")
                return
            page_id=res[0]
            page=get_model("cms.page").browse(page_id)
            if page.state=="inactive":
                self.redirect("/cms_page_not_found")
                return
            ctx["page"]=page
            tmpl_name=page.template or "cms_page"
            content=render(tmpl_name,ctx)
            ctx["content"]=content
            html=render("cms_layout",ctx)
            self.write(html)
            db.commit()
        except:
            import traceback
            traceback.print_exc()
            db.rollback()

Page.register()
