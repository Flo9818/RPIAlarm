import {Component, OnInit} from '@angular/core';
import {BackendService} from '../backend.service';
import {LogTableDataSource} from '../log-table/log-table-datasource';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {MatSnackBar} from '@angular/material';

@Component({
  selector: 'app-action',
  templateUrl: './action.component.html',
  styleUrls: ['./action.component.scss']
})
export class ActionComponent implements OnInit {
  status: any;
  mutedUser: any;

  constructor(private backend: BackendService, private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.getUser();
  }

  getUser() {
    this.backend.getStatus().subscribe(status => this.status = status);
    this.backend.getMutedUsers().subscribe(mutedUser => this.mutedUser = mutedUser);
  }

  reset() {
    this.backend.resetUser().subscribe((res: HttpResponse<any>) => {
      this.snackBar.open('Successfully unmuted all user', 'Dismiss', {
        duration: 2000,
      });
      this.getUser();
    }, (error: HttpErrorResponse) => {
      this.snackBar.open(`${error.status}: ${error.message}`, 'Dismiss', {
        duration: 2000,
      });
    });
  }

  trigger(user: string) {
    this.backend.trigger(user).subscribe((res: HttpResponse<any>) => {
      this.snackBar.open(`Successfully trigger ${user}`, 'Dismiss', {
        duration: 2000,
      });
      this.getUser();
    }, (error: HttpErrorResponse) => {
      this.snackBar.open(`${error.status}: ${error.message}`, 'Dismiss', {
        duration: 2000,
      });
    });
  }

}
