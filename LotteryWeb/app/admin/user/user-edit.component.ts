import { Component, ViewChild, OnInit, Input } from '@angular/core';

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

 
  public showUserEditModal(selectedUser):void {
    this.selectedUser =  selectedUser;
    this.userEdit.show();
    this.persLoading = 'fired';
    this.getUser(this.selectedUser.uid);
  }
 
  public hideUserEditModal():void {
    this.userEdit.hide();
  }

  public PersEditEnable():void {
    this.persEdit = !this.persEdit;
  }

  public AddressEditEnable():void {
    this.addrEdit = !this.addrEdit;
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
}