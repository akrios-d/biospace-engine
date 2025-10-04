import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PublicationService, Publication } from '../../services/publication.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-publications',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './publications.component.html',
  styleUrls: ['./publications.component.scss']
})
export class PublicationsComponent implements OnInit {
  publications: Publication[] = [];
  filter: string = '';

  constructor(private pubService: PublicationService) {}

  ngOnInit(): void {
    this.pubService.getPublications().subscribe(data => this.publications = data);
  }

  filteredPublications(): Publication[] {
    if (!this.filter) return this.publications;
    return this.publications.filter(pub =>
      pub.title.toLowerCase().includes(this.filter.toLowerCase()) ||
      (pub.categories && pub.categories.some(c => c.toLowerCase().includes(this.filter.toLowerCase()))) ||
      (pub.tags && pub.tags.some(t => t.toLowerCase().includes(this.filter.toLowerCase())))
    );
  }
}
