import { BrowserModule }        from '@angular/platform-browser';
import { NgModule }             from '@angular/core';
import { RouterModule } from '@angular/router';

import { MenuProfileComponent }      from './menu-profile.component';

@NgModule({
  declarations: [ MenuProfileComponent ],
  imports:      [ BrowserModule, RouterModule ],
  exports:      [ MenuProfileComponent ],
  providers:    [],
  bootstrap:    [ MenuProfileComponent ]
})
export class MenuProfileModule { }

