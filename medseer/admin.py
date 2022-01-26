from django.contrib import admin

from .models import Journal, Organization, Author, Paper


class PaperInline(admin.TabularInline):
    model = Paper
    fields = ('title', 'doi', 'url')
    extra = 1


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    date_hierarchy = 'modified_at'
    fieldsets = (
        (None,               {'fields': ('name', 'rank')}),
        ('Date information', {'classes': ('collapse',),
                              'fields': ('created_at', 'modified_at')}),
    )
    inlines = (PaperInline,)
    list_display = ('name', 'rank', 'created_at', 'modified_at')
    list_display_links = ('name', 'rank')
    list_filter = ('rank', 'created_at', 'modified_at')
    ordering = ('name', '-rank', '-created_at', '-modified_at')
    readonly_fields = ('created_at', 'modified_at')
    search_fields = ('name', 'rank')


class AuthorInline(admin.TabularInline):
    model = Author
    extra = 1


@ admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    date_hierarchy = 'modified_at'
    fieldsets = (
        (None,               {'fields': ('name', 'rank')}),
        ('Date information', {'classes': ('collapse',),
                              'fields': ('created_at', 'modified_at')}),
    )
    inlines = (AuthorInline,)
    list_display = ('name', 'rank', 'created_at', 'modified_at')
    list_display_links = ('name', 'rank')
    list_filter = ('rank', 'created_at', 'modified_at')
    ordering = ('name', '-rank', '-created_at', '-modified_at')
    readonly_fields = ('created_at', 'modified_at')
    search_fields = ('name', 'rank')


@ admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    date_hierarchy = 'modified_at'
    fieldsets = (
        (None,               {
            'fields': (('forename', 'surname'), 'email', 'organization')}),
        ('Date information', {
            'classes': ('collapse',),
            'fields': ('created_at', 'modified_at')}),
    )
    list_display = ('__str__', 'forename', 'surname', 'email',
                    'organization', 'created_at', 'modified_at')
    list_display_links = ('__str__', 'organization')
    list_editable = ('forename', 'surname', 'email')
    list_filter = ('organization', 'created_at', 'modified_at')
    ordering = ('forename', 'surname', '-created_at', '-modified_at')
    readonly_fields = ('created_at', 'modified_at')
    search_fields = ('name', 'rank')


@ admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True
    date_hierarchy = 'modified_at'
    fieldsets = (
        (None,                {
            'fields': ('pdf', 'tei')}),
        ('Paper information', {
            'fields': ('title', 'abstract', 'journal', 'doi', 'url', 'authors')}),
        ('Date information',  {
            'classes': ('collapse',),
            'fields': ('created_at', 'modified_at')}),
    )
    filter_horizontal = ('authors',)
    list_display = ('title', 'doi', 'url', 'journal',
                    'created_at', 'modified_at')
    list_display_links = ('title', 'doi')
    list_filter = ('authors', 'journal', 'created_at', 'modified_at')
    ordering = ('title', '-created_at', '-modified_at')
    readonly_fields = ('created_at', 'modified_at')
    search_fields = ('title', 'abstract', 'doi', 'url', 'authors', 'journal')
