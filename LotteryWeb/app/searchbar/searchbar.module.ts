import { BrowserModule }    from '@angular/platform-browser';
import { NgModule }         from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'; 

import { SearchBarComponent }  from './searchbar.component';


@NgModule({
  declarations: [ SearchBarComponent ],
  imports:      [ BrowserModule, FormsModule, ReactiveFormsModule ],
  exports:      [ SearchBarComponent ],
  providers:    [ ],
  bootstrap:    [ SearchBarComponent ]
})
export class SearchBarModule { }

