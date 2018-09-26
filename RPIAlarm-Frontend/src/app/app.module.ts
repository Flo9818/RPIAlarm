import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {
  MatTableModule,
  MatPaginatorModule,
  MatSortModule,
  MatTabsModule,
  MatToolbarModule,
  MatButtonModule,
  MatProgressSpinnerModule, MatSnackBarModule, MatCardModule, MatListModule, MatInputModule, MatIconModule, MatTooltipModule
} from '@angular/material';
import {LogTableComponent} from './log-table/log-table.component';
import {HttpClientModule} from '@angular/common/http';
import { ActionComponent } from './action/action.component';
import {AppRoutingModule} from './app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    LogTableComponent,
    ActionComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatTabsModule,
    MatToolbarModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatCardModule,
    MatListModule,
    MatInputModule,
    MatIconModule,
    MatTooltipModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
