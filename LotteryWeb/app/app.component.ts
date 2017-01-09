import { Component, ViewContainerRef } from '@angular/core';
import { ComponentsHelper } from 'ng2-bootstrap/ng2-bootstrap';

ComponentsHelper.prototype.getRootViewContainerRef = function () {
    // https://github.com/angular/angular/issues/9293
    if (this.root) {
        return this.root;
    }
    var comps = this.applicationRef.components;
    if (!comps.length) {
        throw new Error("ApplicationRef instance not found");
    }
    try {
        /* one more ugly hack, read issue above for details */
        var rootComponent = this.applicationRef._rootComponents[0];
        //this.root = rootComponent._hostElement.vcRef;
        this.root = rootComponent._component.viewContainerRef;
        return this.root;
    }
    catch (e) {
        throw new Error("ApplicationRef instance not found");
    }
};


@Component({
  selector: 'app-root',
  templateUrl: 'app/app.component.html',
  styleUrls: ['app/app.component.css']
})

export class AppComponent {
  private viewContainerRef: ViewContainerRef;

  public constructor(viewContainerRef: ViewContainerRef) {
      this.viewContainerRef = viewContainerRef;
  }
}
