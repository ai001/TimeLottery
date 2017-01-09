import { Component, OnInit, ViewChild } from '@angular/core';

import { UserEditComponent } from './user-edit.component';
import { AdminUserService } from './admin-user.service';
import { User } from './user';

@Component({
  selector: 'admin',
  templateUrl: 'app/admin/user/admin-user.component.html',
  styleUrls: ['app/admin/user/admin-user.component.css'],
  providers: [ AdminUserService ]
})

export class AdminUserComponent implements OnInit {
  status: string;
  loading: string = 'init';
  selectedUser: User;
  errorMessage: string;
  users: User[];
  
  @ViewChild(UserEditComponent) userEdit: UserEditComponent

  // ng2-table related configuration
  private data:Array<User> = [];
  public rows:Array<User> = [];
  public page:number = 1;
  public itemsPerPage:number = 10;
  public maxSize:number = 5;
  public numPages:number = 1;
  public length:number = 0;
  public columns:Array<any> = [
    {title: 'Email', name: 'email', sort: true, filtering: {filterString: '', placeholder: 'Filter by email'}},
    {title: 'First Name', name: 'first_name', filtering: {filterString: '', placeholder: 'Filter by first name'}},
    {title: 'Last Name', name: 'last_name', filtering: {filterString: '', placeholder: 'Filter by last name'}},
    {title: 'Created', name: 'created'},
    {title: 'Email Verified', name: 'email_verified'},
    {title: 'Failed Logins', name: 'failed_logins'},
    {title: 'User Banned', name: 'user_banned', className: ['1text-danger', '1glyphicon', '1glyphicon-ban-circle']},
    {title: 'User Restricted', name: 'user_restricted', className: ['1glyphicon', '1glyphicon-resize-small']}
  ];
  public config:any = {
    paging: true,
    sorting: {columns: this.columns},
    filtering: {filterString: ''},
    className: ['table-striped', 'table-bordered']
  };

  //_modal = null;

  //bindModal(modal) {this._modal=modal;}

  constructor(private _adminuserService: AdminUserService) {}

  ngOnInit(): void {
    this.loading = 'fired';
    this.getUsers();
    // this.users = this._adminuserService.getMockUsers();
    // this.length = this.users.length;
    // this.data = this.users;
    // this.onChangeTable(this.config);
  }

  getUsers()  {
    this._adminuserService.getUsers()
                          .subscribe(
                            users => (
                              this.length = users.length,
                              this.data = users,
                              this.onChangeTable(this.config), 
                              this.loading = 'loaded'
                              ),
                            error => (
                              this.errorMessage = <any>error,
                              this.loading = 'error'
                              )
                          );
  }


  public changePage(page:any, data:Array<User> = this.data):Array<User> {
    let start = (page.page - 1) * page.itemsPerPage;
    let end = page.itemsPerPage > -1 ? (start + page.itemsPerPage) : data.length;
    return data.slice(start, end);
  }

  public changeSort(data:any, config:any):any {
    if (!config.sorting) {
      return data;
    }

    let columns = this.config.sorting.columns || [];
    let columnName:string = void 0;
    let sort:string = void 0;

    for (let i = 0; i < columns.length; i++) {
      if (columns[i].sort !== '' && columns[i].sort !== false) {
        columnName = columns[i].name;
        sort = columns[i].sort;
      }
    }

    if (!columnName) {
      return data;
    }

    // simple sorting
    return data.sort((previous:any, current:any) => {
      if (previous[columnName] > current[columnName]) {
        return sort === 'desc' ? -1 : 1;
      } else if (previous[columnName] < current[columnName]) {
        return sort === 'asc' ? -1 : 1;
      }
      return 0;
    });
  }

  public changeFilter(data:any, config:any):any {
    let filteredData:Array<any> = data;
    this.columns.forEach((column:any) => {
      if (column.filtering) {
        filteredData = filteredData.filter((item:any) => {
          return item[column.name].match(column.filtering.filterString);
        });
      }
    });

    if (!config.filtering) {
      return filteredData;
    }

    if (config.filtering.columnName) {
      return filteredData.filter((item:any) =>
        item[config.filtering.columnName].match(this.config.filtering.filterString));
    }

    let tempArray:Array<any> = [];
    filteredData.forEach((item:any) => {
      let flag = false;
      this.columns.forEach((column:any) => {
        if (item[column.name].toString().match(this.config.filtering.filterString)) {
          flag = true;
        }
      });
      if (flag) {
        tempArray.push(item);
      }
    });
    filteredData = tempArray;

    return filteredData;
  }

  public onChangeTable(config:any, page:any = {page: this.page, itemsPerPage: this.itemsPerPage}):any {
    if (config.filtering) {
      Object.assign(this.config.filtering, config.filtering);
    }

    if (config.sorting) {
      Object.assign(this.config.sorting, config.sorting);
    }

    let filteredData = this.changeFilter(this.data, this.config);
    let sortedData = this.changeSort(filteredData, this.config);
    this.rows = page && config.paging ? this.changePage(page, sortedData) : sortedData;
    this.length = sortedData.length;
  }

  public onCellClick(data: any): any {
    this.selectedUser = data.row;

    // Open user edit model
    this.userEdit.showUserEditModal(data.row);

  }

}
