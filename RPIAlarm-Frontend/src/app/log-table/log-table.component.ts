import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {MatPaginator, MatSnackBar, MatSort} from '@angular/material';
import {LogTableDataSource} from './log-table-datasource';
import {BackendService} from '../backend.service';
import {DatePipe} from '@angular/common';
import {registerLocaleData} from '@angular/common';
import localeDe from '@angular/common/locales/de';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';

registerLocaleData(localeDe);


@Component({
  selector: 'app-log-table',
  templateUrl: './log-table.component.html',
  styleUrls: ['./log-table.component.scss']
})
export class LogTableComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  display = false;
  noContent = false;
  dataSource: LogTableDataSource;
  pipe = new DatePipe('de-DE');

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['date', 'time', 'user', 'action'];

  constructor(private backend: BackendService, private snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.getLogs();
  }

  getLogs() {
    this.backend.getLogs().subscribe(logs => {
      if (logs.length === 0) {
        this.noContent = true;
      }  else {
        this.noContent = false;
        this.display = true;
        setTimeout(() => {
          this.paginator.length = logs.length;
          this.dataSource = new LogTableDataSource(this.paginator, this.sort, logs);
        }, 50);
      }
    });
  }

  deleteLog() {
    this.backend.deleteLog().subscribe((res: HttpResponse<any>) => {
      this.snackBar.open('Successfully deleted logs', 'Dismiss', {
        duration: 2000,
      });
      this.getLogs();
    }, (error: HttpErrorResponse) => {
      this.snackBar.open(`${error.status}: ${error.message}`, 'Dismiss', {
        duration: 2000,
      });
    });
  }
}
