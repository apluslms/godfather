$(function () {
    $('#id_members').aplusSearchSelect();
});


function openDialog() {
    $('#light')[0].style.display = 'block';
    $('#fade')[0].style.display = 'block';
}

function closeDialog() {
    $('#light')[0].style.display = 'none';
    $('#fade')[0].style.display = 'none';
}

function addAdmin(admin) {
    if (!$("#id_administrators option[value= " + admin.attr("data-value") + "]").length) {
        $("#id_administrators").append(new Option(admin.text().trim(), admin.attr("data-value")));
        $("#id_administrators option[value= " + admin.attr("data-value") + "]").prop('selected', true);
    }
}

function removeAdmin(admin) {
    var admin = admin.attr("data-value");
    $("#id_administrators option[value= " + admin + "]").remove();
}


(function ($, window, document, undefined) {
    "use strict";

    var pluginName = "aplusSearchSelect";
    var defaults = {
        widget_selector: "#search-select-widget",
        field_selector: 'input[type="text"]',
        search_selector: '.dropdown-toggle',
        result_selector: '.search-options',
        selection_selector: '.search-selected',
    };

    function AplusSearchSelect(element, options) {
        this.element = $(element);
        this.timeout = null;
        if (this.element.prop("tagName") == "SELECT" && this.element.prop("multiple")) {
            this.settings = $.extend({}, defaults, options);
            this.init();
        }
    }

    $.extend(AplusSearchSelect.prototype, {

        init: function () {
            this.widget = $(this.settings.widget_selector).clone()
                .removeAttr("id").removeClass("hide").insertBefore(this.element);
            this.element.hide();
            var self = this;
            this.selection = this.widget.find(this.settings.selection_selector);
            this.selection_li = this.selection.find("li").remove();
            this.element.find("option:selected").each(function (index) {
                self.addSelection($(this).attr("value"), $(this).text());
            });
            this.result = this.widget.find(this.settings.result_selector);
            this.field = this.widget.find(this.settings.field_selector)
                .on("keypress", function (event) {
                    if (event.keyCode == 13) {
                        event.preventDefault();
                        self.searchOptions(true);
                    }
                }).on("keyup", function (event) {
                    if (event.keyCode != 13) {
                        clearTimeout(self.timeout);
                        self.timeout = setTimeout(function () {
                            self.searchOptions(true);
                            self.field.focus();
                        }, 500);
                    }
                });
            this.search = this.widget.find(this.settings.search_selector)
                .on("show.bs.dropdown", function (event) {
                    self.searchOptions();
                });
            this.element.parents("form").on("submit", function (event) {
                self.finish();
            });
        },

        searchOptions: function (show_dropdown) {
            if (show_dropdown && this.result.is(":visible") === false) {
                this.search.find("button").dropdown("toggle");
                return;
            }
            this.result.find("li:not(.not-found)").remove();
            this.result.find("li.not-found").hide();
            var selector = "option";
            var query = this.field.val().trim();
            if (query.length > 0) {
                selector += ":contains(" + this.field.val() + ")";
            }
            var opt = this.element.find(selector);
            if (opt.size() === 0) {
                this.result.find("li.not-found").show();
            } else {
                var self = this;
                opt.slice(0, 20).each(function (index) {
                    var li = $('<li><a data-value="' + $(this).attr("value") + '">' + $(this).text() + '</a></li>');
                    li.find("a").on("click", function (event) {
                        self.addSelection($(this).attr("data-value"), $(this).text());
                    });
                    self.result.append(li);
                });
            }
        },

        addSelection: function (value, name) {
            if (this.selection.find('[data-value="' + value + '"]').size() === 0) {
                var li = this.selection_li.clone();
                var self = this;
                li.find(".name").text(name);
                li.find("button").attr("data-value", value).on('click', function (event) {
                    openDialog();
                    document.getElementById('removeMember').onclick = function (event) {
                        li.find("button").attr("data-value", value).parent("li").remove();
                        removeAdmin(li.find("button").attr("data-value", value));
                        closeDialog();
                    }

                    document.getElementById('setAdmin').onclick = function (event) {
                        addAdmin(li.find("button").attr("data-value", value));
                        closeDialog();
                    }

                    document.getElementById('unsetAdmin').onclick = function (event) {
                        removeAdmin(li.find("button").attr("data-value", value));
                        closeDialog();
                    }


                });
                this.selection.append(li);
            }
        },

        resetSelection: function (values) {
            this.selection.empty();
            var self = this;
            $.each(values, function (index, value) {
                var opt = self.element.find('option[value="' + value + '"]');
                if (opt.size() == 1) {
                    self.addSelection(value, opt.text());
                }
            });
        },

        finish: function () {
            this.widget.remove();
            var select = this.element.show();
            select.find("option:selected").prop("selected", false);
            this.selection.find("button").each(function (index) {
                select.find('option[value="' + $(this).attr("data-value") + '"]').prop("selected", true);
            });
        }
    });

    $.fn[pluginName] = function (options, selectValues) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName, new AplusSearchSelect(this, options));
            }
            if (selectValues) {
                $.data(this, "plugin_" + pluginName).resetSelection(selectValues);
            }
        });
    };

})(jQuery, window, document);