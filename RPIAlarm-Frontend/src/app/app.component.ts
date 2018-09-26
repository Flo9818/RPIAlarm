import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'RPIAlarm';
  links = ['Control', 'Log'];
  activeLink: string;

  constructor() {}

  ngOnInit() {
    this.activeLink = window.location.pathname.split('/')[1];
  }
}
