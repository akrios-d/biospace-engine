import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
    <div class="container mx-auto p-4">
      <h1 class="text-3xl font-bold mb-4">{{ title() }}</h1>
    </div>
  `,
  styleUrls: ['./app.scss']
})
export class App {
  protected readonly title = signal('ExoLexis');
}
