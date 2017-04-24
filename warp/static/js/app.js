function createSubparserAction(action) {
    var column = $("<li/>").addClass("action");//.addClass("column small-12 medium-12")
    //var card = $("<div/>").addClass("card action").appendTo(column);
    var label = $("<label/>", {for: action['uuid']}).appendTo(column);
    var center = $("<center/>").appendTo(label);
    if(action["dest"] !== "==SUPPRESS=="){
        var header = $("<b/>").text(action["dest"].toUpperCase()).appendTo(center);
    }

    var tab_bar = $("<ul/>",{ id: action['uuid'] }).attr('data-tabs', '').addClass("tabs subparser")
        .appendTo(center);

    var tab_content = $("<div data-tabs-content='" + action['uuid'] + "'/>").addClass("tabs-content subparser").appendTo(center);
    $.each(action['choices'], function(name, choice) {
        console.log("Go for choice " + name);
        var li = $("<li/>").addClass("tabs-title").appendTo(tab_bar);
        var link = $("<a/>", { href: '#' + choice['uuid'] }).data({
            name: action['dest'],
            value: name
        }).text(name).appendTo(li);

        var content_div = $("<div/>", { id: choice['uuid'] })
            .addClass("tabs-panel").appendTo(tab_content);
        choice['actions'].forEach(function(action) {
            content_div.append(createAction(action));
        });
    });
    tab_bar.children(":first").addClass('is-active').attr("aria-selected", true);
    tab_content.children(":first").addClass('is-active');
    return column;
}

function createCheckboxAction(action) {
    var switch_div = $("<div/>").addClass("switch");
    var input = $("<input/>", {
        id: action["uuid"],
        type: 'checkbox',
        name: action['uuid']
    }).addClass('switch-input').data("name", action['dest']).appendTo(switch_div);
    var paddle = $("<label/>", {for: action["uuid"]}).addClass("switch-paddle")
        .appendTo(switch_div);
    if(action['checked'] === true) {
        input.attr('checked', true);
    }
    return switch_div
}

function createSubtractableInput(action) {
    var group = $("<div/>").addClass("input-group");
    var input = createSingleInput(action).addClass("input-group-field").appendTo(group);
    var button = $("<a/>").addClass("button rembutton input-group-button").attr("href", "#").appendTo(group).click(function(e) {
        e.preventDefault();
        if(!$(this).prop('disabled')) {
            group.remove();
        }
    });
    var rmIcon = $("<i/>").addClass("fi-minus").appendTo(button);
    return group;
}

function appendInput(div, action, addButton) {
    console.log("Appending input");
    createSubtractableInput(action).insertBefore(addButton);
}

function createPlusInput(action) {
    var div = $("<div/>");
    createSingleInput(action).appendTo(div);
    var addButton = $("<a/>").attr("href", "#").addClass("button addbutton float-right").appendTo(div)
        .click(function(e) {
            e.preventDefault();
            if(!$(this).prop('disabled')) {
                createSubtractableInput(action).insertBefore(addButton);
            }
        });
    var addIcon = $("<i/>").addClass("fi-plus").appendTo(addButton);
    return div;
}

function createStarInput(action) {
    var div = $("<div/>");
//    createSubtractableInput(action).appendTo(div);
    var addButton = $("<a/>").attr("href", "#").addClass("button addbutton float-right").appendTo(div)
        .click(function(e) {
            e.preventDefault();
            if(!$(this).prop('disabled')) {
                createSubtractableInput(action).insertBefore(addButton);
            }
        });
    var addIcon = $("<i/>").addClass("fi-plus").appendTo(addButton);
    return div;
}

function createSingleInput(action) {
    return $('<input/>', {
        name: action['uuid'],
        type: (action['type'] === 'int'?"number":"text")
    }).data("name", action['dest']);
}

function createInputAction(action) {
    if(Number.isInteger(action['nargs']) && action['nargs'] > 1) {
        var div = $("<div/>");
        for(var i = 0; i < action["nargs"]; i++) {
            $('<input/>', {
                name: action['uuid'],
                type: (action['type'] === 'int'?"number":"text")
            }).data("name", action['dest']).appendTo(div);
        }
        return div;
    } else if(action['nargs'] === '*') {
        return createStarInput(action);
    } else if(action['nargs'] === '+') {
        return createPlusInput(action);
    } else {
        return createSingleInput(action);
    }
}

function createAction(action) {
    if('choices' in action) {
        return createSubparserAction(action)
    } else {
        var li = $("<li/>",{'id': 'action-' + action['uuid']}).addClass("action");
        var row = $("<div/>").addClass("row").appendTo(li);
        var helpdiv = $("<div/>").addClass("columns small-2").appendTo(row);
        var labeldiv = $("<div/>").addClass("columns small-3").appendTo(row);
        var label = $("<label/>", {for: action['uuid']}).addClass("middle").appendTo(labeldiv);
        var header = $("<b/>").text(action["dest"].toUpperCase()).appendTo(label);

        var inputdiv = $("<div/>").addClass("columns small-5").appendTo(row)
        var deldiv = $("<div/>").addClass("columns small-2").appendTo(row);
        if(action['is_const']) {
            createCheckboxAction(action).addClass("float-right").appendTo(inputdiv);
        } else {
            createInputAction(action).addClass("float-right").appendTo(inputdiv);
        }
        if(action.desc !== null) {
            var help = $("<button/>", {"type": "button", "data-open": 'modal_' + action['uuid']})
                .addClass("button helpbutton secondary")
                .text("?").appendTo(helpdiv);
            var modal = $("<div/>", {'id': 'modal_' + action['uuid'], "data-reveal":'reveal'})
                .addClass('reveal').appendTo(helpdiv);
            var text = $("<span/>").text(action['desc']).appendTo(modal);
        } else {
            var help = $("<button/>").attr("type", "button").addClass("button disabled secondary").text("?").appendTo(helpdiv);
        }
        if(action.optional === true) {
            var del = $("<button/>").attr("type", "button").addClass("button delbutton alert").html("&times;").appendTo(deldiv);
            del.click(function() {
                thisli = $('#action-' + action['uuid']);
                if(thisli.prop('disabled')) {
                    console.log('tock');
                    thisli.prop('disabled', false);
                    $("#action-" + action['uuid'] + " input").prop('disabled', false).removeClass("disabled");
                    $("#action-" + action['uuid'] + " .addbutton").removeClass('disabled').prop('disabled', false);
                    $("#action-" + action['uuid'] + " .rembutton").removeClass('disabled').prop('disabled', false);
                } else {
                    thisli.prop('disabled', true);
                    $("#action-" + action['uuid'] + " input").prop('disabled', true).addClass('disabled');
                    $("#action-" + action['uuid'] + " .addbutton").addClass('disabled').prop('disabled', true);
                    $("#action-" + action['uuid'] + " .rembutton").addClass('disabled').prop('disabled', true);
                }
            })
        } else {
            var del = $("<button/>").attr("type", "button").addClass("button disabled alert").html("&times;").appendTo(deldiv);
        }
        return li;
    }
}

function createGroup(group) {
    var column = $('<li/>');
    var tab_bar = $("<ul/>",{ id: group['uuid'] }).attr('data-tabs', '').addClass("tabs group").appendTo(column);
    var tab_content = $("<div data-tabs-content='" + group['uuid'] + "'/>").addClass("tabs-content group").appendTo(column);
    group['actions'].forEach(function(action) {
        console.log("Adding action " + action['name'] + " to group");
        var li = $("<li/>").addClass("tabs-title").appendTo(tab_bar);
        var link = $("<a/>", { href: '#' + action['uuid'] }).text(action['name']).appendTo(li);
        var content_div = $("<div/>", { id: action['uuid'] })
            .addClass("tabs-panel").appendTo(tab_content);
        var center = $("<center/>").appendTo(content_div);
        createAction(action).appendTo(center);
    });
    tab_bar.children(":first").addClass('is-active').attr("aria-selected", true);
    tab_content.children(":first").addClass('is-active');
    return column;
}

window.onload = function() {
    $.getJSON("/arguments", function(json) {
        json['groups'].forEach(function(group) {
            console.log("Adding a group");
            $("#actions").append(createGroup(group));
        });
        json['actions'].forEach(function(action) {
            console.log("Adding " + action['dest']);
            $("#actions").append(createAction(action));
        });
        $(document).foundation()
    });
    oboe('/output.json').node('output.*', function(e){
        if(e.type === "err") {
            printErr(e.line);
        } else {
            printOut(e.line);
        }
    });

};

function printOut(data) {
    $("#output").append("<span class=\"out\">" + data + "</span><br />" );
    $("#output").scrollTop($("#output")[0].scrollHeight);
}

function printErr(data){
    $("#output").append("<span class=\"err\">" + data + "</span><br />" );
    $("#output").scrollTop($("#output")[0].scrollHeight);
}

function resumeProcess() {
    $("#resumeButton").css('display', 'none');
    $("#sendButton").css('display', 'inline-block');
    $("#pauseButton").removeClass("disabled").prop('disabled', false);
    $.get({url: '/resume'});
    printErr("Process resumed")
}

function pauseProcess() {
    $("#sendButton").css('display', 'none');
    $("#resumeButton").css('display', 'inline-block');
    $("#pauseButton").addClass("disabled").prop('disabled', true);
    $.get({url: '/pause'});
    printErr("Process paused")
}

function reloadProcess() {
    $("#sendButton").removeClass("disabled").prop('disabled', false);
    $("#stopButton").addClass("disabled").prop('disabled', true);//css('display', 'inline-block');
    $("#pauseButton").addClass("disabled").prop('disabled', true);//css('display', 'inline-block');
    $("#reloadButton").addClass("disabled").prop('disabled', true);//css('display', 'inline-block');
    $.get({url: '/reload',
        success: function() {
            oboe('/output.json').node('output.*', function(e){
                if(e.type === "err") {
                    printErr(e.line);
                } else {
                    printOut(e.line);
                }
            });
    }});
}

function stopProcess() {
    $("#stopButton").addClass("disabled").prop('disabled', true);//css('display', 'none');
    $("#reloadButton").removeClass("disabled").prop('disabled', false);//css('display', 'inline-block');
    $.get({url: '/stop'});
}

function sendData() {
    $("#sendButton").addClass("disabled").prop('disabled', true);
    $("#stopButton").removeClass("disabled").prop('disabled', false);//css('display', 'inline-block');
    $("#pauseButton").removeClass("disabled").prop('disabled', false);//css('display', 'inline-block');
    console.log(calcParams());
    $.post({
        url: '/arguments', 
        data: calcParams(),
        dataType: 'json'
    });
}

function addParam(params, object) {
    params[$(object).data('name')] = [];
    if($(object).attr('type') === "checkbox") {
        params[$(object).data('name')] = object.checked;
    } else {
        var inputs = $('input[name=\''+$(object).attr('name')+'\']');
        inputs.each(function() {
            params[$(this).data('name')].push(this.value);
        });
    }
}

function calcParams() {
    var params = {};
    $('.group input:visible').not(".disabled").each(function() {
        addParam(params, this);
    });

    $('.tabs.subparser .is-active a:visible').not(".disabled").each(function() {
        console.log($(this).data('name') + ": " + $(this).data('value'));
        params[$(this).data('name')]= [$(this).data('value')];
    });
    $('.subparser input:visible').not(".disabled").each(function() {
        addParam(params, this);
    });
    $('.action input').not(".tabs-content input").not(".disabled").each(function() {
        addParam(params, this);
    });
    return params;
}
