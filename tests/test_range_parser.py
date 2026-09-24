import pytest
from src.core.splitter import parse_range_string

def test_parse_single_pages():
    assert parse_range_string("1", 10) == [0]
    assert parse_range_string("1, 3, 5", 10) == [0, 2, 4]
    
def test_parse_ranges():
    assert parse_range_string("1-3", 10) == [0, 1, 2]
    assert parse_range_string("1-3, 5-6", 10) == [0, 1, 2, 4, 5]
    
def test_parse_mixed():
    assert parse_range_string("1, 3-5, 8", 10) == [0, 2, 3, 4, 7]
    
def test_parse_out_of_bounds():
    # Sınır dışı indeksleri görmezden gelmeli veya kelepçelemeli
    assert parse_range_string("9-15", 10) == [8, 9]
    assert parse_range_string("12", 10) == []
    
def test_parse_keywords():
    assert parse_range_string("hepsi", 5) == [0, 1, 2, 3, 4]
    assert parse_range_string("tek", 5) == [0, 2, 4]
    assert parse_range_string("çift", 5) == [1, 3]

def test_parse_invalid_input():
    assert parse_range_string("abc", 10) == []
    assert parse_range_string("1-abc", 10) == []
    assert parse_range_string("", 10) == []
    assert parse_range_string("  ", 10) == []
    
def test_parse_unordered_and_duplicates():
    # Hem gereksiz tekrarları temizlemeli, hem de sıralamalı
    assert parse_range_string("5, 1, 3-3, 1-2", 10) == [0, 1, 2, 4]
