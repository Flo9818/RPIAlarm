import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LogTableComponent} from './log-table/log-table.component';
import {ActionComponent} from './action/action.component';


const routes: Routes = [
  {
    path: 'Log',
    component: LogTableComponent
  },
  {
    path: 'Control',
    component: ActionComponent
  },
  {
    path: '**',
    redirectTo: 'Control'
  }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule {
}
