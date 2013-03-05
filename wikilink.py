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

        # self.view.run_command("expand_selection", {"to": "brackets"})
        #find the word under the cursor
        # word = self.view.substr(location).replace("*", "")
        scope = self.view.substr(self.view.extract_scope(location.a)).replace("*", "")
        scope_name = self.view.scope_name(location.a)

        if "link.external.Wiki" in scope_name or "meta.link.inline.markdown" in scope_name:
                sublime.status_message("try to open " + scope)
                sublime.active_window().run_command('open_url', {"url": scope})

        elif "markup.underline.link.image.markdown" in scope_name:
            sublime.status_message("try to open " + scope)
            sublime.active_window().run_command('open_url', {"url": "file://" + directory + slash + scope})

        elif "link.email.Wiki" in scope_name:
                sublime.status_message("try to mail " + scope)
                sublime.active_window().run_command('open_url', {"url": "mailto:"+scope})
        elif "link.internal.Wiki" in scope_name:
            #okay, we're good. Keep on keepin' on.

            #compile the full file name and path.
            word = scope.replace('[', '').replace(']', '')
            new_file = directory+slash+word+".md"
            #debug section: uncomment to write to the console
            # print "Location: %d" % location.a
            # print "Selected word is '%s'" % word
            # print "Full file path: %s" % new_file
            # print "Selected word scope is '%s'" % self.view.scope_name(location.a)
            # if internalLink in self.view.scope_name(location.a):
            #     print "this is an internal link"
            #end debug section

            if os.path.exists(new_file):
                #open the already-created page.
                new_view = window.open_file(new_file)
            else:
                #Create a new file and slap in the default text.
                new_view = window.new_file()
                new_edit = new_view.begin_edit()
                default_text = "# {0}\n\n".format(word)
                new_view.insert(new_edit,0,default_text)
                new_view.end_edit(new_edit)
                new_view.set_name("%s.md" % word)
                new_view.set_syntax_file("Packages/Wiki/WikiMarkdown.tmLanguage")
        else:
            sublime.status_message("Can only open WikiWords, email addresses or web addresses.")
