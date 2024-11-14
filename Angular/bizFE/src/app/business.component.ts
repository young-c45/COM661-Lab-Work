import { Component } from '@angular/core';
import { RouterOutlet, ActivatedRoute } from '@angular/router';
import { DataService } from './data.service';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'business',
    standalone: true,
    imports: [RouterOutlet, CommonModule],
    providers: [DataService],
    templateUrl: './business.component.html',
    styleUrl: './business.component.css'
})
export class BusinessComponent {
    business_list: any;

    constructor(public dataService: DataService,
        public route: ActivatedRoute) { }

    ngOnInit() {
        this.business_list = this.dataService.getBusiness(
            this.route.snapshot.paramMap.get('id'));
    }
}