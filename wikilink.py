import sublime, sublime_plugin, os, re

class WikiLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        #find our current directory
        directory = os.path.split(self.view.file_name())[0]
        #find our current window
        window = self.view.window()
        slash = "\\" if sublime.platform() == "windows" else "/"
        #find the cursor
        location = self.view.sel()[0]

        #find the word under the cursor
        scope = self.view.substr(self.view.extract_scope(location.a)).replace("*", "").replace("[", "").replace("]", "").split("|")[-1]
        scope_name = self.view.scope_name(location.a)

        if "meta.link.inline.markdown" in scope_name:
            url = scope
            if any(scope.startswith(x) for x in ["http://", "https://", "www", "ftp://", "file://"]):
                url = scope
            else:
                url = "file://" + directory + slash + scope
            sublime.status_message("try to open " + url)
            sublime.active_window().run_command('open_url', {"url": url})

        elif "markup.underline.link.image.markdown" in scope_name or "markup.underline.link.file.Wiki" in scope_name:
            sublime.status_message("try to open " + scope)
            sublime.active_window().run_command('open_url', {"url": "file://" + directory + slash + scope})

        elif "link.email.Wiki" in scope_name:
            sublime.status_message("try to mail " + scope)
            sublime.active_window().run_command('open_url', {"url": "mailto:"+scope})

        elif "link.internal.Wiki" in scope_name:
            filepath = directory + slash + scope
            if os.path.exists(filepath) and scope[-3:] != ".md":
                sublime.status_message("try to open " + filepath)
                sublime.active_window().run_command('open_url', {"url": "file://" + filepath})
            else:
                new_file = filepath + ".md"

                if os.path.exists(new_file):
                    #open the already-created page.
                    new_view = window.open_file(new_file)
                else:
                    #Create a new file and slap in the default text.
                    new_view = window.new_file()
                    new_edit = new_view.begin_edit()
                    default_text = "# {0}\n\n".format(scope)
                    new_view.insert(new_edit,0,default_text)
                    new_view.end_edit(new_edit)
                    new_view.set_name("%s.md" % scope)
                    new_view.set_syntax_file("Packages/Wiki/WikiMarkdown.tmLanguage")
        else:
            sublime.status_message("Can only open WikiWords, email addresses or web addresses.")
