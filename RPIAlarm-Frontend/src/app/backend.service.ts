import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams, HttpResponse} from '@angular/common/http';
import {environment} from '../environments/environment';
import {Observable, pipe} from 'rxjs';
import {map} from 'rxjs/operators';
import {LogTableItem} from './log-table/log-table-datasource';
import {DatePipe} from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class BackendService {

  constructor(private http: HttpClient) {
  }


  getLogs(): Observable<LogTableItem[]> {
    return this.http.get<LogTableItem[]>(`${environment.baseUrl}/log`).pipe(map(logs => logs.map(log => {
      return {
        date: new Date(log.date),
        user: log.user,
        action: log.action
      };
    })));
  }

  getStatus(): Observable<any> {
    return this.http.get(`${environment.baseUrl}/status`);
  }

  getMutedUsers(): Observable<any> {
    return this.http.get<any>(`${environment.baseUrl}/mutedUsers`);
  }

  resetUser(): Observable<any> {
    return this.http.put<any>(`${environment.baseUrl}/reset`, '', {
      headers: new HttpHeaders({
        Authorization: 'Bearer secret'
      }),
      params: new HttpParams().set('user', 'Webapp')
    });
  }

  deleteLog(): Observable<any> {
    return this.http.delete<any>(`${environment.baseUrl}/clearLogs`);
  }

  trigger(user: string): Observable<any> {
    return this.http.put<any>(`${environment.baseUrl}/trigger`, '', {
      headers: new HttpHeaders({
        Authorization: 'Bearer secret'
      }),
      params: new HttpParams().set('user', user)
    });
  }
}
