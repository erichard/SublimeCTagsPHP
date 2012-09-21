import sublime
import sublime_plugin
import sys
import os

# Pull in built-in plugin directory
built_in_plugins = os.path.join(sublime.packages_path(), 'CTags')
if not built_in_plugins in sys.path:
    sys.path.append(built_in_plugins)

from ctagsplugin import *

setting = sublime.load_settings('CTagsPHP.sublime-settings').get # (key, None)

######################### IMPORT PHP USE FOR CLASS UNDER CURSOR #########################


def ctags_import_php_use(jump_directly_if_one=False):
    def wrapper(f):
        def command(self, edit, **args):
            view = self.view
            tags_file = find_tags_relative_to(view.file_name())

            result = f(self, self.view, args, tags_file, {})

            if result not in (True, False, None):
                args, display = result
                if not args:
                    return

                def on_select(i):
                    if i != -1:
                        useStmt = re.sub(r"\.php", "", args[i].tag_path[0])
                        useStmt = re.sub(r"[^A-Z]+(.*)", '\\1', useStmt)
                        useStmt = re.sub('/', '\\\\', useStmt)
                        useStmt = "use " + useStmt + ";"

                        region = view.find(r"^\s*use\s+[\w\\]+[;]", 0)
                        if region != None:
                            line = view.line(region)
                            print line
                            line_contents = "\n" + useStmt
                            self.view.insert(edit, line.end(), line_contents)
                            return True

                        region = view.find(r"^\s*namespace\s+[\w\\]+[;{]", 0)
                        if region != None:
                            line = view.line(region)
                            line_contents = '\n\n' + useStmt
                            self.view.insert(edit, line.end(), line_contents)
                            return True

                        region = view.find(r"<\?php", 0)
                        if region != None:
                            line = view.line(region)
                            line_contents = '\n\n' + useStmt
                            self.view.insert(edit, line.end(), line_contents)
                            return True

                (on_select(0) if   jump_directly_if_one and len(args) == 1
                              else view.window().show_quick_panel(
                                                  display, on_select))
        return command
    return wrapper


class ImportUseCommand(sublime_plugin.TextCommand):
    is_enabled = check_if_building

    def is_visible(self):
        return setting("show_context_menus")

    @ctags_import_php_use(jump_directly_if_one=True)
    def run(self, view, args, tags_file, tags):
        symbol = view.substr(view.word(view.sel()[0]))

        if re.match(r"\w", symbol) == None:
            return status_message('Not a valid symbol "%s" !' % symbol)

        region = view.find(r"^\s*use\s+[\w\\]+" + symbol + "[;]", 0)
        if region != None:
            return status_message('Use for "%s" already exist !' % symbol)

        for tags_file in alternate_tags_paths(view, tags_file):
            tags = (TagFile(tags_file, SYMBOL)
                            .get_tags_dict(symbol,
                                            filters=compile_filters(view)))
            if tags:
                break

        if not tags:
            return status_message('Can\'t find "%s"' % symbol)

        current_file = view.file_name().replace(dirname(tags_file) + os.sep, '')

        def definition_cmp(a, b):
            if normpath(a.tag_path[0]) == current_file:
                return -1
            if normpath(b.tag_path[0]) == current_file:
                return 1
            return 0

        def_filters = compile_definition_filters(view)

        def pass_def_filter(o):
            for f in def_filters:
                for k, v in f.items():
                    if re.match(v, o[k]):
                        return False
            return True

        @prepared_4_quickpanel()
        def sorted_tags():
            p_tags = filter(pass_def_filter, tags.get(symbol, []))
            if not p_tags:
                status_message('Can\'t find "%s"' % symbol)
            p_tags = sorted(p_tags, key=iget('tag_path'))
            if setting('definition_current_first', False):
                p_tags = sorted(p_tags, cmp=definition_cmp)
            return p_tags

        return sorted_tags


class ImportNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        region = self.view.find(r"^\s*namespace\s[\w\\]+;", 0)

        if region != None:
            return status_message('namespace definition already exist !')

        # Filename to namespace
        filename = self.view.file_name()

        if (not filename.endswith(".php")):
            sublime.error_message("No .php extension")
            return

        # namespace begin at first camelcase dir
        namespaceStmt = os.path.dirname(filename)

        if (setting("start_dir_pattern")):
            pattern = re.compile(setting("start_dir_pattern"))
        else:
            pattern = r"[^A-Z]+(.*)"

        namespaceStmt = re.sub(pattern, '\\1', namespaceStmt)
        namespaceStmt = re.sub('/', '\\\\', namespaceStmt)

        region = self.view.find(r"<\?php", 0)
        if region != None:
            line = self.view.line(region)
            line_contents = '\n\n' + "namespace " + namespaceStmt + ";"
            self.view.insert(edit, line.end(), line_contents)
            return True
