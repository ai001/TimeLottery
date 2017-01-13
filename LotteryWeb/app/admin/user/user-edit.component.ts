import { Component, ViewChild, OnInit, Input } from '@angular/core';
import * as moment from 'moment';

import { UserEditService } from './user-edit.service';

// User schema
import { User } from './user';
import { UserDetail } from './userdetail';
 
// todo: change to ng2-bootstrap
import { ModalDirective } from 'ng2-bootstrap/ng2-bootstrap';
 
@Component({
  selector: 'user-edit',
  templateUrl: 'app/admin/user/user-edit.component.html',
  styleUrls: ['app/admin/user/user-edit.component.css'],
  providers:  [UserEditService]
})

export class UserEditComponent implements OnInit {
  @ViewChild('userEdit') public userEdit:ModalDirective;
  private selectedUser: User;
  persLoading: string = 'init';
  userDetail: UserDetail;
  errorMessage: string;
  persEdit: boolean = false;
  addrEdit: boolean = false;

  public dt: Date = new Date();
  public minDate: Date = void 0;
  public events: any[];
  public tomorrow: Date;
  public afterTomorrow: Date;
  public dateDisabled: {date: Date, mode: string}[];

 
  public showUserEditModal(selectedUser):void {
    this.selectedUser =  selectedUser;
    this.userEdit.show();
    this.persLoading = 'fired';
    this.getUser(this.selectedUser.uid);
  }
 
  public hideUserEditModal():void {
    delete this.userDetail;
    this.userEdit.hide();
  }

  public PersEditEnable():void {
    this.persEdit = !this.persEdit;
  }

  public AddressEditEnable():void {
    this.addrEdit = !this.addrEdit;
  }

  public GenderChange(gender):void {
    this.userDetail.gender = gender;
  }

  constructor(private _usereditService: UserEditService) {}

  ngOnInit(): void {}

  getUser(uid: string)  {
    this._usereditService.getUser(uid)
                         .subscribe(
                              userDetail => (
                                this.userDetail = userDetail,
                                this.persLoading = 'loaded'
                              ),
                              error => (
                                this.errorMessage = <any>error,
                                this.persLoading = 'error'
                              )
                        );
  }




  //// datepicker bits

    public dt: Date = new Date();
  public minDate: Date = void 0;
  public events: any[];
  public tomorrow: Date;
  public afterTomorrow: Date;
  public dateDisabled: {date: Date, mode: string}[];
  public formats: string[] = ['DD-MM-YYYY', 'YYYY/MM/DD', 'DD.MM.YYYY',
    'shortDate'];
  public format: string = this.formats[0];
  public dateOptions: any = {
    formatYear: 'YY',
    startingDay: 1
  };
  private opened: boolean = false;
 
  public constructor() {
    (this.tomorrow = new Date()).setDate(this.tomorrow.getDate() + 1);
    (this.afterTomorrow = new Date()).setDate(this.tomorrow.getDate() + 2);
    (this.minDate = new Date()).setDate(this.minDate.getDate() - 1000);
    (this.dateDisabled = []);
    this.events = [
      {date: this.tomorrow, status: 'full'},
      {date: this.afterTomorrow, status: 'partially'}
    ];
  }
 
  public getDate(): number {
    return this.dt && this.dt.getTime() || new Date().getTime();
  }
 
  public today(): void {
    this.dt = new Date();
  }
 
  public d20090824(): void {
    this.dt = moment('2009-08-24', 'YYYY-MM-DD')
      .toDate();
  }
 
  public disableTomorrow(): void {
    this.dateDisabled = [{date: this.tomorrow, mode: 'day'}];
  }
 
  // todo: implement custom class cases
  public getDayClass(date: any, mode: string): string {
    if (mode === 'day') {
      let dayToCheck = new Date(date).setHours(0, 0, 0, 0);
 
      for (let event of this.events) {
        let currentDay = new Date(event.date).setHours(0, 0, 0, 0);
 
        if (dayToCheck === currentDay) {
          return event.status;
        }
      }
    }
 
    return '';
  }
 
  public disabled(date: Date, mode: string): boolean {
    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
  }
 
  public open(): void {
    this.opened = !this.opened;
  }
 
  public clear(): void {
    this.dt = void 0;
    this.dateDisabled = undefined;
  }
 
  public toggleMin(): void {
    this.dt = new Date(this.minDate.valueOf());
  }

}