import { bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app';
import { provideHttpClient } from '@angular/common/http';  // <-- PROVIDE HTTP

bootstrapApplication(App, {
  providers: [
    provideHttpClient(),   // must provide HttpClient globally
  ]
})
.catch(err => console.error(err));
