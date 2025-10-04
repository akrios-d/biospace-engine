import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { PublicationsComponent } from './components/publications/publications.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [PublicationsComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})
export class App {
  protected readonly title = signal('ExoLexis');
}
