import { Component, Input, Output, ElementRef, EventEmitter, AfterViewInit } from '@angular/core';

declare var $: any;// this is very importnant (to work this line: this.modalEl.modal('show')) - don't do this (becouse this owerride jQuery which was changed by bootstrap, included in main html-body template): let $ = require('../../../../../node_modules/jquery/dist/jquery.min.js');

@Component({
  selector: 'user-edit-modal',
  //templateUrl: 'app/admin/user/user-edit-modal.component.html',
  template: `<div class="modal inmodal fade" id="{{modal_id}}" tabindex="-1" role="dialog"  aria-hidden="true" #thisModal>
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header" [ngClass]="{'hide': !(has('mhead') || title) }">
                <button *ngIf="showClose" type="button" class="close" (click)="closeInternal()"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                <ng-content select="mhead"></ng-content>
                <h4 *ngIf='title' class="modal-title">{{ title }}</h4>
            </div>
            <div class="modal-body">
                <ng-content></ng-content>
            </div>

            <div class="modal-footer" [ngClass]="{'hide': !has('mfoot') }" >
                <ng-content select="mfoot"></ng-content>
            </div>
        </div>
    </div>
</div>`
})
export class UserEditModal implements AfterViewInit {

    private _uid = null;
    @Input() title:string;
    @Input() showClose:boolean = true;
    @Output() onClose: EventEmitter<any> = new EventEmitter();

    modalEl = null;
    id: string = uniqueId('modal_');

    constructor(private _rootNode: ElementRef) {}

    open(_uid) {
        this.modalEl.modal('show');
        console.log(_uid);
    }

    close() {
        this.modalEl.modal('hide');
    }

    closeInternal() { // close modal when click on times button in up-right corner
        this.onClose.next(null); // emit event
        this.close();
    }

    ngAfterViewInit() {
        this.modalEl = $(this._rootNode.nativeElement).find('div.modal');
    }

    has(selector) {
        return $(this._rootNode.nativeElement).find(selector).length;
    }
}

let modal_id: number = 0;
export function uniqueId(prefix: string): string {
    return prefix + ++modal_id;
}