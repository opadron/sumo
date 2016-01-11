
(function(exports) {

"use strict";

function isNull(x) {
    return (x === null || x === (void 0));
}

function DynamicPanels(selector) {
    this.container = $(selector).first();
    this.gridster = this.container.children("ul").first().gridster({
        widget_margins: [2, 2],
        widget_base_dimensions: [25, 25],
        min_cols: 0,
        min_rows: 0,
        max_size_x: false,
        widget_selector: "li",
        avoid_overlapped_widgets: true,
        resize: { enabled: true }
    }).data("gridster");
}

DynamicPanels.prototype.add = function add(elements) {
    var self = this;
    elements.each(function(_, elem) {
        self.gridster.add_widget($("<li>").append(elem), 5, 5, 1, 1);
    });

    // NOTE(opadron): add event trigger for new panels
    // ...

    // NOTE(opadron): there must be a better way to make sure the containing
    // <ul> is properly resized.
    this.container.find("> ul > li").each(function(_, elem) {
        self.gridster.resize_widget($(elem));
    });
};

exports.DynamicPanels = DynamicPanels;

})(this);

