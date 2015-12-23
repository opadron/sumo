
(function(exports) {

"use strict";

function isNull(x) {
    return (x === null || x === (void 0));
}

function IdAllocator() {
    this.numAllocated = 0;
    this.freeList = [];
    this.freeSet = {};
}

IdAllocator.prototype.constructor = IdAllocator;

IdAllocator.prototype.alloc = function alloc() {
    var result = (this.freeList.length > 0 ?
                    this.freeList.splice(0, 1)[0] :
                    this.numAllocated++);

    delete this.freeSet[result];
    return result;
};

IdAllocator.prototype.free = function free(i) {
    if(i in this.freeSet) { return; }
    this.freeSet[i] = null;
    this.freeList.push(i);
};

var MAX_COLUMNS = 4;

function DynamicPanelRow(element, parent) {
    this.element = element;
    this.parent = parent;
    this.element.data("row-reference", this);
}

DynamicPanelRow.prototype.constructor = DynamicPanelRow;

DynamicPanelRow.prototype.append = function append() {
    var functionProvided = (arguments.length &&
                            typeof arguments[0] === "function");

    var children = this.element.children("div");
    var numColumns = children.length;

    var oldSize = null;
    var newSize = null;

    var oldClass = null;
    var newClass = null;
    var i;

    if(numColumns >           0) { oldSize = Math.floor(12/(numColumns    )); }
    if(numColumns < MAX_COLUMNS) { newSize = Math.floor(12/(numColumns + 1)); }

    if(isNull(newSize)) {
        throw new Error(
            "Cannot exceed maximum number of columns (" + MAX_COLUMNS + ").");
    }

    if(!isNull(oldSize)) { oldClass = "col-md-" + oldSize; }
    if(!isNull(newSize)) { newClass = "col-md-" + newSize; }

    if(oldSize !== newSize) {
        if(!isNull(oldSize)) { children.removeClass(oldClass); }
        if(!isNull(newSize)) { children.addClass(newClass); }
    }

    var panel = ($("<div>")
                    .addClass("panel-body"));

    var id = this.parent.idAllocator.alloc();
    var self = this;

    var newElement = (
        $("<div>")
            .addClass(newClass)
            .addClass("dynamic-panel-column")
            .attr("id", id)
            .append(
                $("<div>")
                    .addClass("panel")
                    .addClass("panel-default")
                    .addClass("dynamic-panel-panel")
                    .addClass("inside")
                    .append(
                        $("<button>")
                            .addClass("btn")
                            .addClass("btn-danger")
                            .addClass("btn-xs")
                            .addClass("hidden")
                            .addClass("dynamic-panel-close-button")
                            .append(
                                $("<span>")
                                    .addClass("glyphicon")
                                    .addClass("glyphicon-remove"))
                            .append(
                                $(document.createTextNode(" ")))
                            .on("click", function() {
                                self.remove(self.element.children("div#" + id));
                            }))
                    .on({
                        mouseenter: function() {
                            $(this).children("button").removeClass("hidden");
                        },
                        mouseleave: function() {
                            $(this).children("button").addClass("hidden");
                        }
                    })
                    .append(panel)));

    if(newSize === 12) {
        this.element.append($("<button>")
            .addClass("btn")
            .addClass("btn-success")
            .addClass("btn-sm")
            .addClass("dynamic-panel-split-button")
            .append(
                $("<span>")
                    .addClass("glyphicon")
                    .addClass("glyphicon-menu-hamburger")
                    .addClass("rotate-90"))
            .append(
                $(document.createTextNode(" ")))
            .on("click", function() {
                self.append(function(panel) {
                    $(self.parent).triggerHandler("new-panel", [panel]);
                });
            }));

    /* no more room for columns on this row */
    } else if(numColumns === MAX_COLUMNS - 1) {
        (this.element.children("button.dynamic-panel-split-button")
            .addClass("hidden"));
    }

    this.element.append(newElement);

    if(functionProvided) {
        arguments[0].apply(this, [panel]);
    } else {
        panel.append.apply(panel, arguments);
    }

    return this;
};


DynamicPanelRow.prototype.remove = function remove(target) {
    target = target || this.element.children("div");

    var numColumns = this.element.children("div").length;
    var numToRemove = target.filter("div").length;

    var oldSize;
    var newSize;

    var oldClass;
    var newClass;

    oldSize = Math.floor(12/numColumns);
    if(numColumns > numToRemove) {
        newSize = Math.floor(12/(numColumns - numToRemove));
    }

    if(!isNull(oldSize)) { oldClass = "col-md-" + oldSize; }
    if(!isNull(newSize)) { newClass = "col-md-" + newSize; }

    if(oldSize !== newSize) {
        var siblings = target.siblings("div");
        if(!isNull(oldSize)) { siblings.removeClass(oldClass); }
        if(!isNull(newSize)) { siblings.addClass(newClass); }
    }

    var self = this;
    target.each(function(_, x) {
        self.parent.idAllocator.free(Number.parseInt(x.id));
    });

    /* need to enable the split button, again */
    if(numColumns === MAX_COLUMNS) {
        (this.element.children("button.dynamic-panel-split-button")
            .removeClass("hidden"));
    }

    if(isNull(newSize)) { /* no more columns in this row */
        this.element.remove();
    } else {
        target.remove();
    }

    return this;
};


function DynamicPanels(selector) {
    this.element = $(selector).first();
    this.idAllocator = new IdAllocator();

    var self = this;
    this.addRowDiv = (
        $("<div>")
            .addClass("text-center")
            .append(
                $("<button>")
                    .addClass("btn")
                    .addClass("btn-primary")
                    .addClass("glyphicon")
                    .addClass("glyphicon-plus")
                    .text(" ")
                    .on("click", function() {
                        self.append(self.row().append(function(panel) {
                            $(self).triggerHandler("new-panel", [panel]);
                        }));
                    })));

    this.element.append(this.addRowDiv);
}

DynamicPanels.prototype.constructor = DynamicPanels;

DynamicPanels.prototype.row = function row() {
    return new DynamicPanelRow($("<div>").addClass("row"), this);
};

DynamicPanels.prototype.append = function append(row) {
    this.addRowDiv.before(row.element);
    return this;
};

function EXTRACT_ROW_REFERENCES(_, x) { return $(x).data("row-reference"); }

DynamicPanels.prototype.children = function children(filter) {
    return (this.element
                .children("div.row")
                .filter(filter)
                .map(EXTRACT_ROW_REFERENCES));
};

DynamicPanels.prototype.remove = function remove(idList) {
    if(!Array.isArray(idList)) { idList = [idList]; }

    var self = this;
    var target = $(idList.map(function(id) {
        return (self.element
                    .children("div.row")
                    .children("div#" + id)
                    .first()[0]);
    }).filter(Boolean));

    var targetRows = target.parent().map(EXTRACT_ROW_REFERENCES);

    targetRows.each(function(_, row) {
        row.remove(row.element.children().filter(target));
    });

    return this;
};

exports.DynamicPanels = DynamicPanels;
exports.IdAllocator = IdAllocator;

})(this);

