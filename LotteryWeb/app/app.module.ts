import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpModule, JsonpModule } from '@angular/http';
import { Ng2BootstrapModule } from 'ng2-bootstrap/ng2-bootstrap';
//import { Angular2FontawesomeModule } from 'angular2-fontawesome/angular2-fontawesome';

import { AppComponent }   from './app.component';
import { NavbarModule }   from './navbar/navbar.module';
import { HomeModule }     from './home/home.module';
import { SearchBarModule }     from './searchbar/searchbar.module';
import { navbarRouting }  from './navbar/navbar.routing'
import { mainRouting }    from './app.routing'


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    HttpModule,
    JsonpModule,
    Ng2BootstrapModule,
    //Angular2FontawesomeModule,
    NavbarModule,
    HomeModule,
    SearchBarModule,
    navbarRouting,
    mainRouting,
  ],
  providers: [],
  bootstrap: [AppComponent]
})

export class AppModule { }