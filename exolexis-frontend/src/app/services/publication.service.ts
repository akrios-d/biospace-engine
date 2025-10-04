import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Publication {
  _id: string;
  title: string;
  abstractText?: string | null;
  categories?: string[];
  tags?: string[];
  link: string;
}

@Injectable({
  providedIn: 'root'
})
export class PublicationService {
  private apiUrl = 'http://localhost:8081/api/publications';
  constructor(private http: HttpClient) {}
  getPublications(): Observable<Publication[]> {
    return this.http.get<Publication[]>(this.apiUrl);
  }
}
