import { BrowserModule }    from '@angular/platform-browser';
import { NgModule }         from '@angular/core';
import { Ng2TableModule }   from 'ng2-table/ng2-table';
import { PaginationModule } from 'ng2-bootstrap/ng2-bootstrap';
import { ModalModule } from 'ng2-bootstrap/ng2-bootstrap';
import { Angular2FontawesomeModule } from 'angular2-fontawesome/angular2-fontawesome';
import { AdminUserComponent }  from './admin-user.component';

import { UserEditComponent } from './user-edit.component';


@NgModule({
  declarations: [ AdminUserComponent, UserEditComponent ],
  imports:      [ BrowserModule,
                  ModalModule,
                  Ng2TableModule,
                  PaginationModule, 
                  Angular2FontawesomeModule 
                ],
  exports:      [ AdminUserComponent ],
  providers:    [],
  bootstrap:    [ AdminUserComponent ]
})
export class AdminUserModule { }

