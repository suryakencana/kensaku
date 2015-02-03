/**
 * Created by surya on 27/01/15.
 */
// chain multiple helpers
// ex: {{chain 'help1' 'help' kontent}}
Handlebars.registerHelper('chain', function() {
  var helpers = [];
  var args = Array.prototype.slice.call(arguments);
  var argsLength = args.length;
  var index;
  var arg;

  for (index = 0, arg = args[index];
       index < argsLength;
       arg = args[++index]) {
    if (Handlebars.helpers[arg]) {
      helpers.push(Handlebars.helpers[arg]);
    } else {
      args = args.slice(index);
      break;
    }
  }

  while (helpers.length) {
    args = [helpers.pop().apply(Handlebars.helpers, args)];
  }

  return args.shift();
});

//  Highlighter text
//  usage: {{cahaya kontent term='shining'}}
Handlebars.registerHelper('cahaya', function(context, block) {
    return context.replace(new RegExp(".*(" + block.hash.term + ").*", "i"),
        function(a, b) {
            return a.replace(new RegExp(b, "ig"),
                    '<span style="font-weight:bold;">' + b + "</span>");
        });
});

kensaku.keyCode = {
    ALT: 18,
    BACKSPACE: 8,
    CAPS_LOCK: 20,
    COMMA: 188,
    COMMAND: 91,
    COMMAND_LEFT: 91,
    COMMAND_RIGHT: 93,
    CONTROL: 17,
    DELETE: 46,
    DOWN: 40,
    END: 35,
    ENTER: 13,
    ESCAPE: 27,
    HOME: 36,
    INSERT: 45,
    LEFT: 37,
    MENU: 93,
    NUMPAD_ADD: 107,
    NUMPAD_DECIMAL: 110,
    NUMPAD_DIVIDE: 111,
    NUMPAD_ENTER: 108,
    NUMPAD_MULTIPLY: 106,
    NUMPAD_SUBTRACT: 109,
    PAGE_DOWN: 34,
    PAGE_UP: 33,
    PERIOD: 190,
    RIGHT: 39,
    SHIFT: 16,
    SPACE: 32,
    TAB: 9,
    UP: 38,
    WINDOWS: 91
};