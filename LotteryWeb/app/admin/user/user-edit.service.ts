import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { User } from './user';
import { UserDetail } from './userdetail';
//import { USERDETAIL } from './mock-userdetail';

@Injectable()

export class UserEditService {
    private _admin_getUser_URL = 'http://localhost:8080/backend/admin/api/v1/userAdministration/getUserProfile';  // URL to web API

    constructor(private http: Http) { }

    getUser(uid: string): Observable<UserDetail> {
        let bodyString = JSON.stringify({'uid': uid}); // Stringify payload
        let headers    = new Headers({ 'Content-Type': 'application/json' }); // ... Set content type to JSON
        let options    = new RequestOptions({ headers: headers }); // Create a request option
        return this.http.post(this._admin_getUser_URL, bodyString, options)
                                  .map(this.extractData)
                                  .catch(this.handleError);
    }

    // getMockUser(uid: string): Observable<UserDetail> {
    //     return Observable.from(USERDETAIL).map(userDetail => USERDETAIL[0]);
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