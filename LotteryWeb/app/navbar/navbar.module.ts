import { BrowserModule }        from '@angular/platform-browser';
import { NgModule }             from '@angular/core';
import { RouterModule }         from '@angular/router';

import { NavbarComponent }      from './navbar.component';
import { AdminUserModule }    from '../admin/user/admin-user.module';
import { UserProfileModule }    from '../user-profile/user-profile.module';

//import { menu_profileRouting }  from './menu-profile/menu-profile.routing';

@NgModule({
  declarations: [ NavbarComponent ],
  imports:      [ BrowserModule,
                  RouterModule, 
                  //MenuProfileModule, 
                  //menu_profileRouting,
                  AdminUserModule, 
                  UserProfileModule ],
  exports:      [ NavbarComponent ],
  providers:    [],
  bootstrap:    [ NavbarComponent ]
})
export class NavbarModule { }

