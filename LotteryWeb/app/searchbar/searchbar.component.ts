import { Component, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';


@Component({
  selector: 'searchbar',
  templateUrl: 'app/searchbar/searchbar.component.html',
  styleUrls: ['app/searchbar/searchbar.component.css']
})
export class SearchBarComponent {
  searchbarform: FormGroup;

  route_modes = ['Driving', 'Walking', 'Bicycling', 'Transit'];
  route_mode = 'Driving';
  searchbar_data;

  constructor(fb: FormBuilder)  {
    this.searchbarform = fb.group({
      'from_address': ['HA4 8DT'],
      'to_address': ['RG1 8DT'],
      'route_mode': ['Driving'],
      'poi_types': ['Tourist Attractions'],
      'search_area': ['2']
    });
  }

  @Output() onSubmit =  new EventEmitter();

  onGO(value): void {
      this.searchbar_data = { from: value.from_address,
                              to: value.to_address, 
                              poi_types: value.poi_types, 
                              search_area: value.search_area, 
                              mode: this.route_mode }
      this.onSubmit.emit(this.searchbar_data);
  }

  changeMode(value): void {
      this.route_mode = value;
      //this.searchbar_data.mode = value;
      //this.onSubmit.emit(this.searchbar_data);
  }

}
