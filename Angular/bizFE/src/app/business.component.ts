import { Component } from '@angular/core';
import { RouterOutlet, ActivatedRoute } from '@angular/router';
import { DataService } from './data.service';
import { CommonModule } from '@angular/common';
import { GoogleMapsModule } from '@angular/google-maps';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';

@Component({
    selector: 'business',
    standalone: true,
    imports: [RouterOutlet, CommonModule, GoogleMapsModule, 
        ReactiveFormsModule],
    providers: [DataService],
    templateUrl: './business.component.html',
    styleUrl: './business.component.css'
})
export class BusinessComponent {
    business_list: any;
    business_lat: any;
    business_lng: any;
    map_options: google.maps.MapOptions = {};
    map_locations: any[] = [];
    reviewForm: any;

    constructor(public dataService: DataService,
        public route: ActivatedRoute, 
        private formBuilder: FormBuilder) { }

    ngOnInit() {
        this.reviewForm = this.formBuilder.group({
            username: ['', Validators.required],
            comment: ['', Validators.required],
            stars: 5
        })

        this.business_list = this.dataService.getBusiness(
            this.route.snapshot.paramMap.get('id'));
        this.business_lat = this.business_list[0].location.coordinates[0];
        this.business_lng = this.business_list[0].location.coordinates[1];

        this.map_locations.push({
            lat: this.business_lat,
            lng: this.business_lng
        })

        this.map_options = {
            mapId: "DEMO_MAP_ID",
            center: { lat: this.business_lat, lng: this.business_lng },
            zoom: 13,
            disableDefaultUI: true
        };
    }

    onSubmit() {
        this.dataService.postReview(
            this.route.snapshot.paramMap.get('id'),
            this.reviewForm.value);
        this.reviewForm.reset();
    }

    isInvalid(control: any) {
        return this.reviewForm.controls[control].invalid &&
            this.reviewForm.controls[control].touched;
    }

    isUntouched() {
        return this.reviewForm.controls.username.pristine ||
            this.reviewForm.controls.comment.pristine;
    }

    isIncomplete() {
        return this.isInvalid('username') ||
            this.isInvalid('comment') ||
            this.isUntouched();
    }
}