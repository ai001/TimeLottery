import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { User } from './user';
//import { USERS } from './mock-users';

@Injectable()

export class AdminUserService {
    private _admin_getUsers_URL = 'http://localhost:8080/backend/admin/api/v1/userAdministration/getUsers';  // URL to web API

    constructor(private http: Http) { }

    getUsers(): Observable<User[]> {
        return this.http.get(this._admin_getUsers_URL)
                                 .map(this.extractData)
                                 .catch(this.handleError);

        //return USERS;
    }

    // getMockUsers(): Observable<User[]> {
    //     return Observable.from(USERS).map(users => USERS);
    //     //return USERS;
    // }

    private extractData(res: Response) {
        let body = res.json();
        return body.data || {};
    }

    private handleError(error: Response | any) {
        // In a real world app, we might use a remote logging infrastructure
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Observable.throw(errMsg);
    }
}