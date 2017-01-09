import { BrowserModule }    from '@angular/platform-browser';
import { NgModule }         from '@angular/core';

import { UserProfileComponent }  from './user-profile.component';


@NgModule({
  declarations: [ UserProfileComponent ],
  imports:      [ BrowserModule ],
  exports:      [ UserProfileComponent ],
  providers:    [],
  bootstrap:    [ UserProfileComponent ]
})
export class UserProfileModule { }

