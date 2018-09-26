import {DataSource} from '@angular/cdk/collections';
import {MatPaginator, MatSort} from '@angular/material';
import {map} from 'rxjs/operators';
import {merge, Observable, of as observableOf} from 'rxjs';
import {DatePipe} from '@angular/common';
import { registerLocaleData } from '@angular/common';
import localeDe from '@angular/common/locales/de';

registerLocaleData(localeDe);

export interface LogTableItem {
  user: string;
  date: Date;
  action: string;
}

/**
 * Data source for the LogTable view. This class should
 * encapsulate all logic for fetching and manipulating the displayed logs
 * (including sorting, pagination, and filtering).
 */
export class LogTableDataSource extends DataSource<LogTableItem> {
  pipe = new DatePipe('de-DE');
  constructor(private paginator: MatPaginator, private sort: MatSort, public logs: LogTableItem[]) {
    super();
  }

  /**
   * Connect this logs source to the table. The table will only update when
   * the returned stream emits new items.
   * @returns A stream of the items to be rendered.
   */
  connect(): Observable<LogTableItem[]> {
    // Combine everything that affects the rendered logs into one update
    // stream for the logs-table to consume.
    const dataMutations = [
      observableOf(this.logs),
      this.paginator.page,
      this.sort.sortChange
    ];

    // Set the paginatordataSource.logss length
    this.paginator.length = this.logs.length;

    return merge(...dataMutations).pipe(map(() => {
      return this.getPagedData(this.getSortedData([...this.logs]));
    }));
  }

  /**
   *  Called when the table is being destroyed. Use this function, to clean up
   * any open connections or free any held resources that were set up during connect.
   */
  disconnect() {}

  /**
   * Paginate the logs (client-side). If you're using server-side pagination,
   * this would be replaced by requesting the appropriate logs from the server.
   */
  private getPagedData(data: LogTableItem[]) {
    const startIndex = this.paginator.pageIndex * this.paginator.pageSize;
    return data.splice(startIndex, this.paginator.pageSize);
  }

  /**
   * Sort the logs (client-side). If you're using server-side sorting,
   * this would be replaced by requesting the appropriate logs from the server.
   */
  private getSortedData(data: LogTableItem[]) {
    if (!this.sort.active || this.sort.direction === '') {
      return data;
    }

    return data.sort((a, b) => {
      const isAsc = this.sort.direction === 'asc';
      switch (this.sort.active) {
        case 'name': return compare(a.user, b.user, isAsc);
        case 'action': return compare(a.action, b.action, isAsc);
        case 'date': return compare(this.pipe.transform(a.date, 'mediumDate'), this.pipe.transform(b.date, 'mediumDate'), isAsc);
        case 'time': return compare(this.pipe.transform(a.date, 'mediumTime'), this.pipe.transform(b.date, 'mediumTime'), isAsc);
        default: return 0;
      }
    });
  }
}

/** Simple sort comparator for example ID/Name columns (for client-side sorting). */
function compare(a, b, isAsc) {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}
